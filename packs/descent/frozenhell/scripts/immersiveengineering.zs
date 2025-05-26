import mods.immersiveintelligence.ChemicalBath;

// Removals
//recipes.removeByRecipeName("immersiveengineering:stone_decoration/blastbrick");
recipes.removeByRecipeName("immersiveengineering:stone_decoration/cokebrick");
recipes.removeByRecipeName("immersiveengineering:stone_decoration/insulating_glass");

// remove sand concrete recipe, so slag is required
recipes.removeByRecipeName("immersiveengineering:stone_decoration/concrete");
// replace main kiln brick sandstone with concrete
recipes.removeByRecipeName("immersiveengineering:stone_decoration/alloybrick");

// Additions
//recipes.addShaped(<immersiveengineering:stone_decoration:1> * 3, [[<minecraft:netherbrick>, <minecraft:brick>, <minecraft:netherbrick>],[<minecraft:brick>, <ore:blockNetherSludge>, <minecraft:brick>], [<minecraft:netherbrick>, <minecraft:brick>, <minecraft:netherbrick>]]);
recipes.addShaped(<immersiveengineering:stone_decoration> * 3, [[<minecraft:clay_ball>, <ore:ingotBrickNether>, <minecraft:clay_ball>], [<ore:ingotBrickNether>, <immersiveengineering:stone_decoration:4>, <ore:ingotBrickNether>], [<minecraft:clay_ball>, <ore:ingotBrickNether>, <minecraft:clay_ball>]]);
recipes.addShaped(<immersiveengineering:stone_decoration:8> * 2, [[<ore:oc:chamelium>, <ore:blockGlass>, <ore:oc:chamelium>], [<ore:dustIron>, <ore:dyeGreen>, <ore:dustIron>], [<ore:oc:chamelium>, <ore:blockGlass>, <ore:oc:chamelium>]]);
recipes.addShaped(<immersiveengineering:stone_decoration:10> * 2, [[<ore:concrete>, <ore:ingotBrick>], [<ore:ingotBrick>, <ore:concrete>]]);

// Add iron dust -> steel for blast furnace
mods.immersiveengineering.BlastFurnace.addRecipe(<immersiveengineering:metal:8>, <ore:dustIron>, 1200, <immersiveengineering:material:7>);

// galvanized steel electroplating
// input, output, fluid, energy, time
ChemicalBath.addRecipe(<immersiveengineering:material:2>, <immersiveengineering:material:28>, <liquid:moltenzinc> * 50, 512, 100); // rod
ChemicalBath.addRecipe(<immersiveengineering:material:23>, <immersiveengineering:material:29>, <liquid:moltenzinc> * 50, 512, 100); // wire
ChemicalBath.addRecipe(<immersiveengineering:metal:8>, <immersiveengineering:metal:41>, <liquid:moltenzinc> * 100, 512, 100); // ingot
ChemicalBath.addRecipe(<immersiveengineering:metal:17>, <immersiveengineering:metal:42>, <liquid:moltenzinc> * 100, 512, 100); // grit  
ChemicalBath.addRecipe(<immersiveengineering:metal:28>, <immersiveengineering:metal:43>, <liquid:moltenzinc> * 15, 512, 100); // nugget
ChemicalBath.addRecipe(<immersiveengineering:metal:38>, <immersiveengineering:metal:44>, <liquid:moltenzinc> * 100, 512, 100); // plate

ChemicalBath.addRecipe(<immersiveengineering:storage:8>, <immersiveengineering:storage:9>, <liquid:moltenzinc> * 900, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:storage_slab:8>, <immersiveengineering:storage_slab:9>, <liquid:moltenzinc> * 450, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:sheetmetal:8>, <immersiveengineering:sheetmetal:11>, <liquid:moltenzinc> * 400, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1:0>, <immersiveengineering:metal_decoration1:8>, <liquid:moltenzinc> * 160, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1:1>, <immersiveengineering:metal_decoration1:9>, <liquid:moltenzinc> * 100, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1:2>, <immersiveengineering:metal_decoration1:10>, <liquid:moltenzinc> * 100, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1:3>, <immersiveengineering:metal_decoration1:11>, <liquid:moltenzinc> * 100, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1_slab:1>, <immersiveengineering:metal_decoration1_slab:9>, <liquid:moltenzinc> * 50, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1_slab:2>, <immersiveengineering:metal_decoration1_slab:10>, <liquid:moltenzinc> * 50, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration1_slab:3>, <immersiveengineering:metal_decoration1_slab:11>, <liquid:moltenzinc> * 50, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration2:0>, <immersiveengineering:metal_decoration2:9>, <liquid:moltenzinc> * 320, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration2:1>, <immersiveengineering:metal_decoration2:10>, <liquid:moltenzinc> * 100, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:metal_decoration2:7>, <immersiveengineering:metal_decoration2:11>, <liquid:moltenzinc> * 160, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:steel_scaffolding_stairs0>, <immersiveengineering:steel_galvanized_scaffolding_stairs0>, <liquid:moltenzinc> * 160, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:steel_scaffolding_stairs1>, <immersiveengineering:steel_galvanized_scaffolding_stairs1>, <liquid:moltenzinc> * 160, 512, 100);
ChemicalBath.addRecipe(<immersiveengineering:steel_scaffolding_stairs2>, <immersiveengineering:steel_galvanized_scaffolding_stairs2>, <liquid:moltenzinc> * 160, 512, 100);
