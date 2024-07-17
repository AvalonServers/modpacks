import com.zeitheron.hammercore.utils.color.ColorHelper;

var colors = 
[
	0xFFFFFF,
	0xFF8B00,
	0xFF25FF,
	0x9EBCFF,
	0xFFFF00,
	0x94FF00,
	0xFF63A6,
	0x757575,
	0xCECFCF,
	0x00C3C3,
	0x8700FF,
	0x1B1BFF,
	0x713800,
	0x0BC300,
	0xED1609,
	0x2E2E2E
];

for(var i = 0; i < 16; ++i)
	colors[i] = ColorHelper.multiply(colors[i], 0.5);

function light(world, pos, tile)
{
	if(tile.isOn())
		add(Light.builder().pos(pos).color(colors[tile.getColor()], false).radius(15).build());
}