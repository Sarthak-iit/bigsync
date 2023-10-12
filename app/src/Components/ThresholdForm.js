import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

function ThresholdForm({ values, setValues, setReadyToCheckEvents }) {
  const [errors, setErrors] = useState({
    stepChange: false,
    oscillatoryEvent: false,
    impulseEvent: false,
    islandingEvent: false,
  });

  const isFloatOrInt = (value) => {
    return !isNaN(value) && (Number.isInteger(value) || !Number.isNaN(parseFloat(value)));
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setValues({
      ...values,
      [name]: value,
    });
  };

  const handleSubmit = () => {
    const newErrors = {
      stepChange: !isFloatOrInt(values.stepChange),
      oscillatoryEvent: !isFloatOrInt(values.oscillatoryEvent),
      impulseEvent: !isFloatOrInt(values.impulseEvent),
      islandingEvent: !isFloatOrInt(values.islandingEvent),
    };
    const hasErrors = Object.values(newErrors).some((error) => error);
    if (!hasErrors) {
        setErrors(newErrors);
        setReadyToCheckEvents(true);
    } else {

      setErrors(newErrors);
    }
  };

  return (
    <div>
      <Grid mt={2} container direction={'column'} spacing={1}>
        <TextField
          required
          error={errors.stepChange}
          helperText={errors.stepChange ? 'Enter a threshold' : ''}
          id="stepChange"
          name="stepChange"
          size="small"
          label="Step Change Threshold"
          value={values.stepChange}
          onChange={handleChange}
        />
        <TextField
          required
          error={errors.oscillatoryEvent}
          helperText={errors.oscillatoryEvent ? 'Enter a threshold' : ''}
          id="oscillatoryEvent"
          name="oscillatoryEvent"
          size="small"
          label="Oscillatory Event Threshold"
          value={values.oscillatoryEvent}
          onChange={handleChange}
        />
        <TextField
          required
          error={errors.impulseEvent}
          helperText={errors.impulseEvent ? 'Enter a threshold' : ''}
          id="impulseEvent"
          name="impulseEvent"
          size="small"
          label="Impulse Event Threshold"
          value={values.impulseEvent}
          onChange={handleChange}
        />
        <TextField
          required
          error={errors.islandingEvent}
          helperText={errors.islandingEvent ? 'Enter a threshold' : ''}
          id="islandingEvent"
          name="islandingEvent"
          size="caption"
          label="Islanding Event Threshold"
          value={values.islandingEvent}
          onChange={handleChange}
        />
        <Button variant="contained" color="primary" size='x' onClick={handleSubmit}>
          Set threshold
        </Button>
      </Grid>
    </div>
  );
}

export default ThresholdForm;
