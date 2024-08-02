// Disable crafting the XNet antenna
// The reason behind this is it would introduce power creep over intended methods of long-distance item transport
// (i.e. trains, or ME Quantum Link bridges)
scripts.shared.blacklist(<xnet:antenna>);
scripts.shared.blacklist(<xnet:antenna_base>);
scripts.shared.blacklist(<xnet:antenna_dish>);
scripts.shared.blacklist(<xnet:wireless_router>);
