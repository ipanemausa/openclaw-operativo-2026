import React from "react";



const InputBase = ({

&#x20; label,

&#x20; type = "text",

&#x20; value,

&#x20; onChange,

&#x20; placeholder,

&#x20; className = "",

&#x20; ...props

}) => {

&#x20; return (

&#x20;   <input

&#x20;     type={type}

&#x20;     value={value}

&#x20;     onChange={onChange}

&#x20;     placeholder={placeholder}

&#x20;     className={

&#x20;       "w-full px-3 py-2 border border-gray-300 rounded-md text-sm " +

&#x20;       "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 " +

&#x20;       className

&#x20;     }

&#x20;     {...props}

&#x20;   />

&#x20; );

};



export default InputBase;



