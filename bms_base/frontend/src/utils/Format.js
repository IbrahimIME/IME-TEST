class Format {
	left_pad(value, length, char) {
		return value.toString().padStart(length, char);
	}

	right_pad(value, length, char) {
		return value.toString().padEnd(length, char);
	}

	amount(value, decimal) {
		return parseFloat(value)
			.toFixed(decimal)
			.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
	}

	date_stamp(date_stamp) {
		try {
			const datestamp = new Date(Date.parse(date_stamp));

			var date = this.left_pad(datestamp.getDate(), 2, "0");
			var month = this.left_pad(datestamp.getMonth() + 1, 2, "0");
			var year = datestamp.getFullYear();

			var formatted_datestamp = date + "/" + month + "/" + year;

			return formatted_datestamp;
		} catch (e) {
			return e;
		}
	}

	datetime_stamp(datetime_stamp) {
		try {
			const datetimestamp = new Date(Date.parse(datetime_stamp));

			var date = this.left_pad(datetimestamp.getDate(), 2, "0");
			var month = this.left_pad(datetimestamp.getMonth() + 1, 2, "0");
			var year = datetimestamp.getFullYear();
			var hour = this.left_pad(datetimestamp.getHours(), 2, "0");
			var minute = this.left_pad(datetimestamp.getMinutes(), 2, "0");
			var second = this.left_pad(datetimestamp.getSeconds(), 2, "0");
			var ampm = datetimestamp.getHours() < 12 ? "AM" : "PM";

			var formatted_datetime_stamp = date + "/" + month + "/" + year + " " + hour + ":" + minute + ":" + second + " " + ampm;

			return formatted_datetime_stamp;
		} catch (e) {
			return e;
		}
	}
}

export default new Format();
