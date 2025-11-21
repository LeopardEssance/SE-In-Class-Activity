function FormInput({ id, label, type, value, onChange, placeholder, disabled }) {
  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required
        disabled={disabled}
      />
    </div>
  );
}

export default FormInput;
