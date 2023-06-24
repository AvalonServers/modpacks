import crafttweaker.block.IBlock;
import crafttweaker.block.IBlockDefinition;

// buff recipes a bit
recipes.removeByRecipeName("railcraft:locomotive_electric#0$1");
recipes.addShaped(<railcraft:locomotive_electric>, [
    [<minecraft:redstone_lamp>, <ore:plateSteel>, null], 
    [<railcraft:charge:5>, <ore:blockChargeBatteryRechargeable>, <railcraft:charge:5>], 
    [<ore:gearSteel>, <minecraft:minecart>, <ore:gearSteel>]
    ]);

// add slightly easier recipes for signalling shit and integrate some stuff
// circuits
// controller: railcraft:circuit:0, 1, 2, 3
recipes.removeByRecipeName("railcraft:circuit#0$1");
recipes.removeByRecipeName("railcraft:circuit#1$1");
recipes.removeByRecipeName("railcraft:circuit#2$1");
recipes.removeByRecipeName("railcraft:circuit#3$1");

recipes.addShapeless(<railcraft:circuit:0> * 2, [<ore:oc:materialCircuitBoardPrinted>, <ore:oc:circuitChip1>, <ore:dyeRed>]);
recipes.addShapeless(<railcraft:circuit:1> * 2, [<ore:oc:materialCircuitBoardPrinted>, <ore:oc:circuitChip1>, <ore:dyeGreen>]);
recipes.addShapeless(<railcraft:circuit:2> * 2, [<ore:oc:materialCircuitBoardPrinted>, <ore:oc:circuitChip1>, <ore:dyeYellow>]);
recipes.addShapeless(<railcraft:circuit:3> * 2, [<ore:oc:materialCircuitBoardPrinted>, <ore:oc:circuitChip1>, <ore:dyeBlue>]);

// allow exchange from railcraft rails to IR vanilla scale rails and vice versa
val irVanillaScale = <immersiverailroading:item_rail_part>.withTag({gauge: 0.632});
recipes.addShapeless(irVanillaScale, [<railcraft:rail>, <railcraft:rail>]);
recipes.addShapeless(<railcraft:rail> * 2, [irVanillaScale]);
