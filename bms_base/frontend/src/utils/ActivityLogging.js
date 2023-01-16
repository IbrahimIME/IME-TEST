import { ActivityLog } from "../endpoints";
import Api from "./Api";
import Cookies from "./Cookies";

async function ActivityLogging(Action, App_Feature = "") {
	let IP,
		State,
		Country = "";

	await fetch("https://geolocation-db.com/json/")
		.then((res) => res.json())
		.then((result) => {
			IP = result.IPv4;
			State = result.state;
			Country = result.country_name;
		});

	let log = {
		User_ID: Cookies.get("User_ID") ? Cookies.get("User_ID") : "",
		Name: Cookies.get("Preferred_Name") ? Cookies.get("Preferred_Name") : "",
		Action: Action,
		App_Feature: App_Feature,
		State: State,
		Country: Country,
		IP: IP,
	};

	await Api.post({
		url: ActivityLog.save_log(),
		body: log,
	}).then((result) => {
		if (!result.success) console.log(result);
	});
}

export default ActivityLogging;
