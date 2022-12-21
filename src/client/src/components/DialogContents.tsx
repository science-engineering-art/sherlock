import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Dialog from '@mui/material/Dialog';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from "@mui/material/Switch";

const model_options = [
  'Boolean',
  'Vector',
  'Fuzzy',
];

const corpus_options = [
  'Cranfield',
  'Vaswani',
  'Cord19',
];

export interface ConfirmationDialogRawProps {
  id: string;
  keepMounted: boolean;
  value: string;
  open: boolean;
  onClose: (value?: string) => void;
}

function ConfirmationDialogModel(props: ConfirmationDialogRawProps) {
  const { onClose, value: valueProp, open, ...other } = props;
  const [value, setValue] = React.useState(valueProp);
  const radioGroupRef = React.useRef<HTMLElement>(null);

  React.useEffect(() => {
    if (!open) {
      setValue(valueProp);
    }
  }, [valueProp, open]);

  const handleEntering = () => {
    if (radioGroupRef.current != null) {
      radioGroupRef.current.focus();
    }
  };

  const handleCancel = () => {
    onClose();
  };

  const handleOk = () => {
    onClose(value);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue((event.target as HTMLInputElement).value);
  };

  return (
    <Dialog
      sx={{ '& .MuiDialog-paper': { width: '80%', maxHeight: 435 } }}
      maxWidth="xs"
      TransitionProps={{ onEntering: handleEntering }}
      open={open}
      {...other}
    >
      <DialogTitle>Model</DialogTitle>
      <DialogContent dividers>
        <RadioGroup
          ref={radioGroupRef}
          aria-label="model"
          name="model"
          value={value}
          onChange={handleChange}
        >
          {model_options.map((option) => (
            <FormControlLabel
              value={option}
              key={option}
              control={<Radio />}
              label={option}
            />
          ))}
        </RadioGroup>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={handleCancel}>
          Cancel
        </Button>
        <Button onClick={handleOk}>Ok</Button>
      </DialogActions>
    </Dialog>
  );
}

function ConfirmationDialogCorpus(props: ConfirmationDialogRawProps) {
  const { onClose, value: valueProp, open, ...other } = props;
  const [value, setValue] = React.useState(valueProp);
  const radioGroupRef = React.useRef<HTMLElement>(null);

  React.useEffect(() => {
    if (!open) {
      setValue(valueProp);
    }
  }, [valueProp, open]);

  const handleEntering = () => {
    if (radioGroupRef.current != null) {
      radioGroupRef.current.focus();
    }
  };

  const handleCancel = () => {
    onClose();
  };

  const handleOk = () => {
    onClose(value);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue((event.target as HTMLInputElement).value);
  };

  return (
    <Dialog
      sx={{ '& .MuiDialog-paper': { width: '80%', maxHeight: 435 } }}
      maxWidth="xs"
      TransitionProps={{ onEntering: handleEntering }}
      open={open}
      {...other}
    >
      <DialogTitle>Corpus</DialogTitle>
      <DialogContent dividers>
        <RadioGroup
          ref={radioGroupRef}
          aria-label="corpus"
          name="corpus"
          value={value}
          onChange={handleChange}
        >
          {corpus_options.map((option) => (
            <FormControlLabel
              value={option}
              key={option}
              control={<Radio />}
              label={option}
            />
          ))}
        </RadioGroup>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={handleCancel}>
          Cancel
        </Button>
        <Button onClick={handleOk}>Ok</Button>
      </DialogActions>
    </Dialog>
  );
}

interface Settings {
  valueModel: string,
  valueCorpus: string,
  setValueModel: Function,
  setValueCorpus: Function
}

export default function ConfirmationDialog(props: Settings) {
  const [openModelsOp, setOpenModelsOp] = React.useState(false);
  const [openCorpusOp, setOpenCorpusOp] = React.useState(false);
  // const [valueModel, setValueModel] = React.useState('Vector');
  // const [valueCorpus, setValueCorpus] = React.useState('Cranfield');

  const handleClickListItemModel = () => {
    setOpenModelsOp(true);
  };

  const handleCloseModel = (newValue?: string) => {
    setOpenModelsOp(false);

    if (newValue) {
      props.setValueModel(newValue);
    }
  };

  const handleClickListItemCorpus = () => {
    setOpenCorpusOp(true);
  };

  const handleCloseCorpus = (newValue?: string) => {
    setOpenCorpusOp(false);

    if (newValue) {
      props.setValueCorpus(newValue);
    }
  };

  const [checked, setChecked] = React.useState(false);

  const handleSwitchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setChecked(event.target.checked);
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 400, bgcolor: 'background.paper' }}>
      <List component="div" role="group">
        <ListItem
          button
          divider
          aria-haspopup="true"
          aria-controls="model-menu"
          aria-label="model"
          onClick={handleClickListItemModel}
        >
          <ListItemText primary="Model" secondary={props.valueModel} />
        </ListItem>
        <ListItem
          button
          divider
          aria-haspopup="true"
          aria-controls="corpus-menu"
          aria-label="corpus"
          onClick={handleClickListItemCorpus}
        >
          <ListItemText primary="Corpus" secondary={props.valueCorpus} />
        </ListItem>

        <ListItem button >
           <FormControlLabel
          value="cluster"
          control={<Switch checked={checked}
          onChange={handleSwitchChange}
          inputProps={{ 'aria-label': 'controlled' }}
        />}
          label="Show clustered results"
          labelPlacement="start"
        />
        </ListItem>

        <ConfirmationDialogModel
          id="model-menu"
          keepMounted
          open={openModelsOp}
          onClose={handleCloseModel}
          value={props.valueModel}
        />
        <ConfirmationDialogCorpus
          id="corpus-menu"
          keepMounted
          open={openCorpusOp}
          onClose={handleCloseCorpus}
          value={props.valueCorpus}
        />
      </List>
    </Box>
  );
}
