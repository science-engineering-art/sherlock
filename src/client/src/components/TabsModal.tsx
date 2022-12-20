import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Icon from '@mui/material/Icon';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Switch from '@mui/material/Switch';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function BasicTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const [checked, setChecked] = React.useState(false);

  const handleSwitchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setChecked(event.target.checked);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example" centered>
          <Tab label="Model" {...a11yProps(0)} />
          <Tab label="Corpus" {...a11yProps(1)} />
          <Tab label="Clustering" {...a11yProps(2)} />
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        <FormControl>
          <FormLabel id="demo-row-radio-buttons-group-label"></FormLabel>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
            >
              <FormControlLabel value="Boolean" control={<Radio />} label="Boolean" />
              <FormControlLabel value="Vector" control={<Radio />} label="Vector" />
              <FormControlLabel value="Fuzzy" control={<Radio />} label="Fuzzy" />
            </RadioGroup>
        </FormControl>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <FormControl>
          <FormLabel id="demo-row-radio-buttons-group-label"></FormLabel>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
            >
              <FormControlLabel value="Cranfield" control={<Radio />} label="Cranfield" />
              <FormControlLabel value="Vaswani" control={<Radio />} label="Vaswani" />
              <FormControlLabel value="Cord19" control={<Radio />} label="Cord19" />
            </RadioGroup>
        </FormControl>
      </TabPanel>
      <TabPanel value={value} index={2}>
        Show clustered results
        <Switch
          checked={checked}
          onChange={handleSwitchChange}
          inputProps={{ 'aria-label': 'controlled' }}
        />
      </TabPanel>
    </Box>
  );
}
