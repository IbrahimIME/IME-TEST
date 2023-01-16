import { Box, List, ListItemButton, ListItemText, Popover, Typography } from "@mui/material";

import i18n from "../../i18n";
import { Cookies } from "../../utils";

function Notification(props) {
	return (
		<Popover
			open={props.show}
			onClose={props.handleClosePopover}
			anchorEl={props.anchorEl}
			anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
			transformOrigin={{ vertical: "top", horizontal: "right" }}
			className="mx-5 mt-4"
		>
			<Box sx={{ backgroundColor: Cookies.get("PrimaryColor"), display: "flex", justifyContent: "center", py: 1 }}>
				<Typography variant="h6" sx={{ color: "white" }}>
					{i18n.t("notifications")}
				</Typography>
			</Box>
			<div className="tab-content" style={{ minWidth: "250px", maxWidth: "500px", maxHeight: "550px", overflowY: "auto" }}>
				{props.notifications.length === 0 && <div className="navi-text text-center py-5">{i18n.t("no_notification")}</div>}
				{props.notifications.length > 0 && (
					<List>
						{props.notifications.map((noti, index) => (
							<ListItemButton
								key={index}
								onClick={() => {
									if (noti.url !== "") props.history.push(noti.url);
									props.handleClosePopover();
								}}
							>
								<ListItemText>{noti.message}</ListItemText>
							</ListItemButton>
						))}
					</List>
				)}
			</div>
		</Popover>
	);
}

export default Notification;
