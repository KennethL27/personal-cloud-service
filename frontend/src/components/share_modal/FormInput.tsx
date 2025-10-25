import React from 'react';

interface FormInputProps {
  id: string;
  label: string;
  type: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  helperText?: string;
}

export function FormInput({
  id,
  label,
  type,
  value,
  onChange,
  error,
  placeholder,
  disabled = false,
  required = false,
  helperText,
}: FormInputProps) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium mb-2">
        {label} {required && '*'}
      </label>
      <input
        type={type}
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className={`w-full px-3 py-2 rounded border focus:outline-none focus:ring-2 ${
          disabled
            ? 'bg-gray-600 text-gray-300 border-gray-500 cursor-not-allowed'
            : `bg-gray-700 text-white ${
                error ? 'border-red-500' : 'border-gray-600'
              } focus:ring-blue-500`
        }`}
        placeholder={placeholder}
      />
      {error && <p className="text-red-400 text-sm mt-1">{error}</p>}
      {helperText && !error && (
        <p className="text-xs text-gray-400 mt-1">{helperText}</p>
      )}
    </div>
  );
}
