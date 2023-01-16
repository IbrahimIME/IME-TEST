import { Popover } from "@mui/material";
import { useState } from "react";

import i18n from "../../i18n";
import { MuiButton, MuiTextField } from "../common";
import { CloseIcon, SearchIcon } from "../Icon";

function Search(props) {
	const [search, setSearch] = useState("");

	const onChangeSearch = (e) => {
		setSearch(e.target.value);
	};

	const handleSearch = () => {
		console.log(search);
	};

	const clearSearch = () => {
		setSearch("");
	};

	const handleKeyDown = (e) => {
		if (e.key === "Enter") handleSearch();
	};

	return (
		<Popover
			open={props.show}
			onClose={() => {
				setSearch("");
				props.handleClosePopover();
			}}
			anchorEl={props.anchorEl}
			anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
			transformOrigin={{ vertical: "top", horizontal: "right" }}
			className="mx-5 mt-4 search-popover"
		>
			<MuiTextField
				size="large"
				placeholder={i18n.t("search")}
				value={search}
				onChange={onChangeSearch}
				onKeyDown={handleKeyDown}
				InputProps={{
					startAdornment: <SearchIcon sx={{ mr: 2 }} />,
					endAdornment: (
						<MuiButton
							tooltip={i18n.t("clear")}
							disabled={search.length > 0 ? false : true}
							mode="icon"
							onClick={clearSearch}
							content={<CloseIcon />}
						/>
					),
				}}
				sx={{ minWidth: "200px", maxWidth: "300px" }}
			/>
		</Popover>
	);
}

export default Search;
