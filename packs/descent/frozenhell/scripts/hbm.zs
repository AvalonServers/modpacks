import mods.immersiveengineering.ArcFurnace;
import mods.thermalexpansion.Factorizer;

// For unknown reasons, these ones don't seem to have Factorizer recipes
Factorizer.addRecipeBoth(<hbm:powder_steel>, <hbm:powder_steel_tiny> * 9);
Factorizer.addRecipeBoth(<hbm:powder_lithium>, <hbm:powder_lithium_tiny> * 9);
Factorizer.addRecipeBoth(<hbm:powder_lanthanium>, <hbm:powder_lanthanium_tiny> * 9);
Factorizer.addRecipeBoth(<hbm:powder_neodymium>, <hbm:powder_neodymium_tiny> * 9);
Factorizer.addRecipeBoth(<hbm:powder_cobalt>, <hbm:powder_cobalt_tiny> * 9);
Factorizer.addRecipeBoth(<hbm:powder_niobium>, <hbm:powder_niobium_tiny> * 9);
Factorizer.addRecipeBoth(<hbm:powder_cerium>, <hbm:powder_cerium_tiny> * 9);

// Same with the arc furnace
ArcFurnace.addRecipe(<hbm:lithium>, <hbm:powder_lithium>, null, 100, 512);
ArcFurnace.addRecipe(<hbm:ingot_lanthanium>, <hbm:powder_lanthanium>, null, 100, 512);
ArcFurnace.addRecipe(<hbm:ingot_neodymium>, <hbm:powder_neodymium>, null, 100, 512);
ArcFurnace.addRecipe(<hbm:ingot_cobalt>, <hbm:powder_cobalt>, null, 100, 512);
ArcFurnace.addRecipe(<hbm:ingot_niobium>, <hbm:powder_niobium>, null, 100, 512);
ArcFurnace.addRecipe(<hbm:ingot_cerium>, <hbm:powder_cerium>, null, 100, 512);
