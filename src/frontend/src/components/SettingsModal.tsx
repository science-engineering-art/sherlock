import * as React from 'react';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import './QueryBar.css'
import ConfirmationDialog from "./DialogContents";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2),
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1),
  },
}));

export interface DialogTitleProps {
  id: string;
  children?: React.ReactNode;
  onClose: () => void;
}

function BootstrapDialogTitle(props: DialogTitleProps) {
  const { children, onClose, ...other } = props;

  return (
    <DialogTitle sx={{ m: 0, p: 2 }} {...other}>
      {children}
      {onClose ? (
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <i className="fa fa-times" aria-hidden="true"></i>
        </IconButton>
      ) : null}
    </DialogTitle>
  );
}

export default function SettingsModal() {
  const [open, setOpen] = React.useState(false);
  
  const [valueModel, setValueModel] = React.useState('Vector');
  const [valueCorpus, setValueCorpus] = React.useState('Cranfield');
  
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
    sessionStorage['model'] = valueModel.toLowerCase();
    sessionStorage['dataset'] = valueCorpus.toLowerCase();
  };

  return (
    <div>
      <button className="searchButton" onClick={handleClickOpen}>
        <i className="fa fa-cog"></i>
      </button>
      <BootstrapDialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <BootstrapDialogTitle id="customized-dialog-title" onClose={handleClose}>
          Settings
        </BootstrapDialogTitle>
        <DialogContent dividers>
          <ConfirmationDialog
            valueModel={valueModel}
            valueCorpus={valueCorpus}
            setValueModel={setValueModel}
            setValueCorpus={setValueCorpus}
          />
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
            Save changes
          </Button>
        </DialogActions>
      </BootstrapDialog>
    </div>
  );
}
