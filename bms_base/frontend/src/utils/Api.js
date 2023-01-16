import Cookies from "./Cookies";

class Api {
	async get(obj) {
		var url = obj.url;
		var headers = obj.headers || {
			"access-token": Cookies.get("token"),
		};

		const result = await fetch(url, {
			headers: headers,
		}).then((res) => res.json());

		return result;
	}

	async post(obj) {
		var url = obj.url;
		var headers = obj.headers || {
			Accept: "application/json",
			"Content-Type": "application/json",
			"access-token": Cookies.get("token"),
		};
		var body = obj.body || null;

		const result = await fetch(url, {
			method: "POST",
			headers: headers,
			body: obj.formData ? obj.formData : JSON.stringify(body),
		}).then((res) => res.json());

		return result;
	}

	async put(obj) {
		var url = obj.url;
		var headers = obj.headers || {
			Accept: "application/json",
			"Content-Type": "application/json",
			"access-token": Cookies.get("token"),
		};
		var body = obj.body || null;

		const result = await fetch(url, {
			method: "PUT",
			headers: headers,
			body: JSON.stringify(body),
		}).then((res) => res.json());

		return result;
	}

	async delete(obj) {
		var url = obj.url;
		var headers = obj.headers || {
			Accept: "application/json",
			"Content-Type": "application/json",
			"access-token": Cookies.get("token"),
		};
		var body = obj.body || null;

		const result = await fetch(url, {
			method: "DELETE",
			headers: headers,
			body: JSON.stringify(body),
		}).then((res) => res.json());

		return result;
	}

	async patch(obj) {
		var url = obj.url;
		var headers = obj.headers || {
			"Content-Type": "application/json",
			"access-token": Cookies.get("token"),
		};
		var body = obj.body || null;

		const result = await fetch(url, {
			method: "PATCH",
			headers: headers,
			body: JSON.stringify(body),
		}).then((res) => res.json());

		return result;
	}
}

export default new Api();
