import Cookie from "universal-cookie";

const cookie = new Cookie();

class Cookies {
	get(key) {
		return cookie.get(key);
	}

	get_all() {
		return cookie.get_all();
	}

	set(key, value) {
		cookie.set(key, value, { path: "/" });
	}

	remove(key) {
		cookie.remove(key, { path: "/" });
	}

	remove_all() {
		var cookies = cookie.get_all();

		for (const c of cookies) {
			cookie.remove(c);
		}
	}
}

export default new Cookies();
