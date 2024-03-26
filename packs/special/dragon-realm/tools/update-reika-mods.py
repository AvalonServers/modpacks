import tomli
import tomli_w
import bs4
import requests
import typing
import zipfile
import os
import io
import argparse
import hashlib
import urllib.parse
import re
import pathlib
import subprocess


class ReikaPackUpdateState(typing.TypedDict):
  reika_mods_updated: int
  other_mods_updated: int
  config_updated: int
  textures_updated: int

  reika_mods_managed_paths: list[str]
  other_mods_managed_paths: list[str]
  config_managed_paths: list[str]
  textures_managed_paths: list[str]


class ReikaPackUpdates(typing.TypedDict):
  cdn_url: str
  mods_url: str
  config_url: str
  texture_url: str
  client_only_mods: list[str]
  server_only_mods: list[str]
  excluded_mods: list[str]
  state: ReikaPackUpdateState


class ReikaPack(typing.TypedDict):
  updates: ReikaPackUpdates


class PackExtendedSpecialConfiguration(typing.TypedDict):
  reika: ReikaPack


class PackExtendedConfiguration(typing.TypedDict):
  special: PackExtendedSpecialConfiguration


class ReikaPackUpdater:
  """
  Special handling for updating externally hosted Reika modpacks, only DR currently uses this
  """
  def __init__(self, root: str):
    self._root = root
    with open(os.path.join(root, 'extra.toml'), 'rb') as f:
      self._pack = tomli.load(f)

  def _fetch_timestamps(self) -> ReikaPackUpdateState:
    timestamps = ReikaPackUpdateState()

    config = self._pack['special']['reika']['updates']

    mods_body = bs4.BeautifulSoup(requests.get(config['mods_url']).content, features='html.parser')
    mods_updates = mods_body.find_all('div', { 'class': 'lastupdate-internal' })
    timestamps['reika_mods_updated'] = int(mods_updates[0].get_text(strip=True))
    timestamps['other_mods_updated'] = int(mods_updates[1].get_text(strip=True))

    config_body = bs4.BeautifulSoup(requests.get(config['config_url']).content, features='html.parser')
    config_updates = config_body.find_all('div', { 'class': 'lastupdate-internal' })
    timestamps['config_updated'] = int(config_updates[0].get_text(strip=True)) # hard mode is the first one

    texture_body = bs4.BeautifulSoup(requests.get(config['texture_url']).content, features='html.parser')
    texture_updates = texture_body.find_all('div', { 'class': 'lastupdate-internal' })
    timestamps['textures_updated'] = int(texture_updates[0].get_text(strip=True))

    return timestamps

  def _generate_mod_slug(self, file_name: str) -> typing.Tuple[str, str]:
    def is_forbidden(c) -> bool:
      return c.isdigit() or c in ['[', ']', '(', ')', '{', '}', '.']

    def slug_segment_not_reject(seg: str) -> bool:
      for _, c in enumerate(seg):
        if is_forbidden(c):
          return False
      return True
    
    def read_str_until_forbidden(seg: str) -> str:
      # if there is both a number and a dot then it's probably some sort of version number
      result = ''
      flag = False
      for _, c in enumerate(seg):
        if is_forbidden(c):
          if flag:
            result = result[0:-1]
            break
          else:
            flag = True
        result += c
      return result

    # any number after a dash or a space should be removed
    file_name = file_name.strip()

    split_fn = re.split(' |-|_', file_name)
    split_fn_c = [read_str_until_forbidden(split_fn[0])] \
      + list(filter(slug_segment_not_reject, split_fn[1:]))

    new_fn = '-'.join(split_fn_c)
    new_fn = re.sub('-{2,}', '-', new_fn).strip('-_ ')

    # fix later... special edge case handling
    if file_name.startswith('StevesFactoryManager'):
      idx = new_fn.rfind('A')
      new_fn = new_fn[0:idx]

    # add dashes
    slug_fn = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1-', new_fn)
    slug_fn = slug_fn.lower().replace(' ', '-').replace("'", '')
    slug_fn = slug_fn.removeprefix('mod_') # fixup for litemods

    return new_fn, slug_fn
  
  def _get_mod_side(self, config: ReikaPackUpdates, slug: str):
    client_only = config.get('client_only_mods', [])
    server_only = config.get('server_only_mods', [])
    if slug in client_only:
      return 'client'
    if slug in server_only:
      return 'server'
    return 'both'
  
  def _update_folder_generic(self, config: ReikaPackUpdates, bytes: io.BytesIO, subdir: str = None, cdn_url: str = None) -> list[str]:
    managed_paths = []
    excluded_paths = config.get('excluded_paths', [])

    with zipfile.ZipFile(bytes) as zip:
      for file in zip.filelist:
        filename = os.path.basename(file.filename)
        if filename.endswith('-disabled'):
          continue

        filename_stem = pathlib.Path(file.filename).stem

        path_main = []
        if subdir is not None:
          path_main.append(subdir)
        path_main.append(os.path.dirname(file.filename))

        dest_path_prefix = ('/'.join(path_main)).strip('/')
        os.makedirs(os.path.join(self._root, dest_path_prefix), exist_ok=True)

        if cdn_url is not None:
          name, slug = self._generate_mod_slug(filename_stem)
          if slug in config.get('excluded_mods', []):
            continue

          file_hash = hashlib.sha256(zip.read(file)).hexdigest()
          packwiz_toml = {
            'name': name,
            'filename': filename,
            'side': self._get_mod_side(config, slug),
            'download': {
              'url': f'{cdn_url}/{urllib.parse.quote(file.filename)}',
              'hash-format': 'sha256',
              'hash': file_hash,
            },
          }

          dest_path = '/'.join([dest_path_prefix, f'{slug}.pw.toml'])
          if dest_path in excluded_paths:
            continue

          dest_path_real = os.path.join(self._root, dest_path)
          with open(dest_path_real, 'wb') as f:
            tomli_w.dump(packwiz_toml, f)
        else:
          dest_path = '/'.join([dest_path_prefix, filename])
          if dest_path in excluded_paths:
            continue

          zip.extract(file, self._root)

        managed_paths.append(dest_path)
    
    return managed_paths

  def _cleanup_managed_paths(self, mp: list[str]):
    config = self._pack['special']['reika']['updates']
    excluded_paths = config.get('excluded_paths', [])

    # remove everything in existing managed paths
    for path in mp:
      if path in excluded_paths:
        continue

      full_path = os.path.join(self._root, path)
      if os.path.exists(full_path):
        os.remove(full_path)
  
  def _update_reika_mods(self, config: ReikaPackUpdates) -> list[str]:
    cdn_url = config['cdn_url'] + '/ReikaMods'
    request = requests.get(config['mods_url'] + '?button1=1')
    return self._update_folder_generic(config, io.BytesIO(request.content), 'mods', cdn_url)

  def _update_other_mods(self, config: ReikaPackUpdates) -> list[str]:
    cdn_url = config['cdn_url'] + '/mods'
    request = requests.get(config['mods_url'] + '?button2=1')
    return self._update_folder_generic(config, io.BytesIO(request.content), 'mods', cdn_url)

  def _update_config(self, config: ReikaPackUpdates) -> list[str]:
    request = requests.get(config['config_url'] + '?button1=1')
    return self._update_folder_generic(config, io.BytesIO(request.content))

  def _update_texture_pack(self, config: ReikaPackUpdates) -> list[str]:
    rpack_name = 'Tyksera 1.7 v24.zip'
    prefix_folder = os.path.join(self._root, 'resourcepacks')
    os.makedirs(prefix_folder, exist_ok=True)

    request = requests.get(config['cdn_url'] + f'/resourcepacks/{rpack_name}')
    with open(os.path.join(prefix_folder, rpack_name), 'wb') as f:
      f.write(request.content)

    return [f'resourcepacks/{rpack_name}']

  def run(self, force=False):
    print('running special updater for dragon realm')

    updates_config = self._pack['special']['reika']['updates']
    if not 'state' in updates_config:
      updates_config['state'] = {}

    updates_state = updates_config['state']
    latest_timestamps = self._fetch_timestamps()

    modified = False

    if force or latest_timestamps['reika_mods_updated'] > updates_state.get('reika_mods_updated', 0):
      print(f'updating reika mods, new timestamp {latest_timestamps["reika_mods_updated"]}')
      self._cleanup_managed_paths(updates_state.get('reika_mods_managed_paths', []))

      updates_state['reika_mods_updated'] = latest_timestamps['reika_mods_updated']
      updates_state['reika_mods_managed_paths'] = self._update_reika_mods(updates_config)
      modified = True
    
    if force or latest_timestamps['other_mods_updated'] > updates_state.get('other_mods_updated', 0):
      print(f'updating other mods, new timestamp {latest_timestamps["other_mods_updated"]}')
      self._cleanup_managed_paths(updates_state.get('other_mods_managed_paths', []))

      updates_state['other_mods_updated'] = latest_timestamps['other_mods_updated']
      updates_state['other_mods_managed_paths'] = self._update_other_mods(updates_config)
      modified = True
    
    if force or latest_timestamps['config_updated'] > updates_state.get('config_updated', 0):
      print(f'updating configuration, new timestamp {latest_timestamps["config_updated"]}')
      self._cleanup_managed_paths(updates_state.get('config_managed_paths', []))

      updates_state['config_updated'] = latest_timestamps['config_updated']
      updates_state['config_managed_paths'] = self._update_config(updates_config)
      modified = True
    
    if force or latest_timestamps['textures_updated'] > updates_state.get('textures_updated', 0):
      print(f'updating texture pack, new timestamp {latest_timestamps["textures_updated"]}')
      self._cleanup_managed_paths(updates_state.get('textures_managed_paths', []))

      updates_state['textures_updated'] = latest_timestamps['textures_updated']
      updates_state['textures_managed_paths'] = self._update_texture_pack(updates_config)
      modified = True
    
    if modified:
      print('timestamps updated, writing modified state file')
      with open(os.path.join(self._root, 'extra.toml'), 'wb') as f:
        tomli_w.dump(self._pack, f)
      
      # tell packwiz to refresh the metadata
      subprocess.run(['git', 'add', '.'])
      subprocess.run(['packwiz', 'refresh'])

      # git add anything changed in the current pack
      subprocess.run(['git', 'add', '.'])


parser = argparse.ArgumentParser(prog='update-reika-mods', description='reika modpack updater')
parser.add_argument('-f', '--force', action='store_true', help='force a pack update', default=False)
args = parser.parse_args()

updater = ReikaPackUpdater(os.curdir)
updater.run(force=args.force)
