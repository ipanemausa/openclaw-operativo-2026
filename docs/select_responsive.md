import React from "react";

const SelectBase = ({
  value,
  onChange,
  options = [],
  className = "",
  ...props
}) => {
  return (
    <select
      value={value}
      onChange={onChange}
      className={
        "w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white " +
        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 " +
        className
      }
      {...props}
    >
      {options.map((opt, index) => (
        <option key={index} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
};

export default SelectBase;

