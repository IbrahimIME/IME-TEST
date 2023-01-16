const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class DAM {
	document_group(ID) {
		return BASE_URL + "/history/document_group/" + ID;
	}

	document_master(ID) {
		return BASE_URL + "/history/document_master/" + ID;
	}

	my_document(ID) {
		return BASE_URL + "/history/my_document/" + ID;
	}
}

export default new DAM();
