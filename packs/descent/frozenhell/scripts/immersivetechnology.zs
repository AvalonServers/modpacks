import mods.immersivetechnology.GasTurbine;

// lower consumption rate for gasoline fuel
GasTurbine.removeFuel(<liquid:gasoline>);
GasTurbine.addFuel(<liquid:fluegas> * 1000, <liquid:gasoline> * 160, 10);
