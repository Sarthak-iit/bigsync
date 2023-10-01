import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'


export default function DiscreteSlider(prop) {
    let windowSize = prop.prop[0];
    let setwindowSize = prop.prop[1];
    const valuetext = (value) => {
        return `${Number(value / 10)} sec`;
    }
    const handleChange = (event, newValue) => { setwindowSize(Number(newValue / 10)); }
    return (
        <Stack spacing={2} direction="row" alignItems="center" justifyContent="center" mt={2}>
            <Typography variant="body1"> Window size:</Typography>
            <Box sx={{ width: 300 }}>
                <Slider
                    aria-label="Temperature"
                    defaultValue={20}
                    onChange={handleChange}
                    valueLabelFormat={valuetext}
                    valueLabelDisplay="auto"
                    step={10}
                    marks
                    min={10}
                    max={200}
                />
            </Box>
            <Typography variant="body1">{windowSize} sec</Typography>


        </Stack>
    );
}