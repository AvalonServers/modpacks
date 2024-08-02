// Add extra ores to the marx generator
import mods.industrialwires.MarxGenerator;

//MarxGenerator.addRecipe(input, double averageRelativeEnergy, double maxMainOutput, mainOutput, [int smallMainRatio, outSmall])

// without IC2 installed, placing these can crash the server
recipes.remove(<industrialwires:general_stuff:3>);
recipes.remove(<industrialwires:general_stuff:5>);
