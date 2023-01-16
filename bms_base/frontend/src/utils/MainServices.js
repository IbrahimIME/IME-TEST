import { Auth } from "../endpoints";
import Api from "./Api";
import Cookies from "./Cookies";

class MainServices {
	async isSystemAdministrator() {
		const result = await Api.get({
			url: Auth.is_system_admin(),
			headers: {
				"access-token": Cookies.get("token"),
				User_ID: Cookies.get("User_ID"),
			},
		});

		if (result.error) {
			console.log(result);
			return false;
		}

		return result["SystemAdministrator"];
	}

	async isSysAdmin(Org_ID, Role_ID, User_ID) {
		const result = await Api.get({
			url: Auth.is_sys_admin(),
			headers: {
				"access-token": Cookies.get("token"),
				Org_ID: Org_ID,
				Role_ID: Role_ID,
				User_ID: User_ID,
			},
		});

		if (result.error) {
			console.log(result);
			return false;
		}

		return result["SysAdmin"];
	}
}

export default new MainServices();
