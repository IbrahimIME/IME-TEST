const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class MAS {
	customer(ID) {
		return BASE_URL + "/history/customer/" + ID;
	}

	currency(ID) {
		return BASE_URL + "/history/currency/" + ID;
	}

	item_group(ID) {
		return BASE_URL + "/history/item_group/" + ID;
	}

	item_master(ID) {
		return BASE_URL + "/history/item_master/" + ID;
	}

	supplier(ID) {
		return BASE_URL + "/history/supplier/" + ID;
	}
}

export default new MAS();
