class Validation {
	isEmpty(value) {
		if (value === null || value === undefined || !value || value.length === 0 || value === "") return true;
		else return false;
	}

	isString(value) {
		if (typeof value === "string") return true;
		else return false;
	}

	isNumber(value) {
		if (typeof value === "number") return true;
		else return false;
	}

	isBoolean(value) {
		if (typeof value === "boolean") return true;
		else return false;
	}

	isDate(value) {
		if (Date.parse(value)) return true;
		else return false;
	}

	isEmail(value) {
		const reg =
			/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

		if (reg.test(String(value).toLowerCase())) return true;
		else return false;
	}

	isURL(value) {
		try {
			var url = new URL(value);

			if (url) return true;
			return false;
		} catch {
			return false;
		}
	}

	isValidLength(value, maxLength = -1) {
		if (maxLength > 0) {
			if (value.toString().length <= maxLength) return true;
			else return false;
		}

		console.log("isValidLength(): No Maximum Length given.");
		return false;
	}
}

export default new Validation();
