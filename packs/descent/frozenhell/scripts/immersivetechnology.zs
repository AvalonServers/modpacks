import mods.immersivetechnology.GasTurbine;

// lower consumption rate for gasoline fuel
GasTurbine.removeFuel(<liquid:gasoline>);
GasTurbine.addFuel(<liquid:fluegas> * 1000, <liquid:gasoline> * 160, 10);

// add creosote oil as a fuel (600mB over 10 ticks, 60mB/t)
GasTurbine.addFuel(<liquid:fluegas> * 1000, <liquid:creosote> * 600, 10);
