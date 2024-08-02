import crafttweaker.item.IItemStack;

// Blacklist an item, removing its recipe and tooltip
// TODO: Also prevent its block from dropping anything or being broken in Survival mode
function blacklist(item as IItemStack) {
  recipes.remove(item);
  item.addTooltip(format.red("This item is disabled. Contact a server admin."));
}
