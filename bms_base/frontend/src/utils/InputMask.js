import React from "react";
import { IMaskInput } from "react-imask";

const configBlocks = {
	currencyRate: {
		mask: Number,
		radix: ".",
		scale: 4,
		signed: true,
		padFractionalZeros: true,
		value: "",
		unmask: true,
	},
};

export const PostcodeMask = React.forwardRef(function PostcodeMask(props, ref) {
	const { onChange, ...other } = props;
	return <IMaskInput {...other} mask="00000" inputRef={ref} onAccept={(value) => onChange({ target: { name: props.name, value } })} overwrite />;
});

export const CurrencyRateMask = React.forwardRef(function CurrencyRateMask(props, ref) {
	const { onChange, ...other } = props;
	return (
		<IMaskInput
			{...other}
			blocks={configBlocks}
			mask="currencyRate"
			inputRef={ref}
			onAccept={(value) => onChange({ target: { name: props.name, value } })}
			overwrite
		/>
	);
});

export const ServerIPMask = React.forwardRef(function ServerIPMask(props, ref) {
	const { onChange, ...other } = props;
	return (
		<IMaskInput
			{...other}
			mask="[00]0.[00]0.[00]0.[00]0"
			inputRef={ref}
			onAccept={(value) => onChange({ target: { name: props.name, value } })}
			overwrite
		/>
	);
});
