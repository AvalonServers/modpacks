# make android station easier to obtain
recipes.remove(<matteroverdrive:android_station>);
recipes.addShaped(<matteroverdrive:android_station>, [
    [<matteroverdrive:tritanium_plate>, <matteroverdrive:tritanium_plate>, <matteroverdrive:tritanium_plate>],
    [<matteroverdrive:isolinear_circuit:1>, <matteroverdrive:forcefield_emitter>, <matteroverdrive:isolinear_circuit:2>],
    [<minecraft:glowstone_dust>, <matteroverdrive:machine_casing>, <minecraft:redstone>]
]);
