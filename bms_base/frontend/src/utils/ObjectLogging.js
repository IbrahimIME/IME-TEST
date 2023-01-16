import { ObjectLog } from "../endpoints";
import Api from "./Api";
import Cookies from "./Cookies";

async function ObjectLogging(Action, Object, Object_ID, Desc = "") {
	const user = Cookies.get("User_ID") ? Cookies.get("User_ID") : "";
	const org = Cookies.get("Org_ID");
	const roles = Cookies.get("Role_ID");
	let IP = "";

	await fetch("https://geolocation-db.com/json/")
		.then((res) => res.json())
		.then((result) => {
			IP = result.IPv4;
		});

	const object_log = {
		User: user,
		Org: org,
		Roles: roles,
		Action: Action,
		Object: Object,
		Object_ID: Object_ID,
		Desc: Desc,
		IP: IP,
	};

	await Api.post({
		url: ObjectLog.save_log(),
		body: object_log,
	}).then((result) => {
		if (!result.success) console.log(result);
	});
}

export default ObjectLogging;
