function QuickBrightnessControls({ onBrightnessChange, disabled, presets = [25, 50, 75, 100] }) {
  return (
    <div className="quick-controls">
      <h4>Quick Settings</h4>
      <div className="quick-buttons">
        {presets.map((preset) => (
          <button
            key={preset}
            className="quick-btn"
            onClick={() => onBrightnessChange(preset)}
            disabled={disabled}
          >
            {preset}%
          </button>
        ))}
      </div>
    </div>
  );
}

export default QuickBrightnessControls;
