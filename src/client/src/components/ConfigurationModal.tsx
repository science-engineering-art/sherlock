import axios from "axios";
import './QueryBar.css'
import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import BasicTabs from "./TabsModal";

function ConfigurationModal() {

  return (
      <div>
          <button
            type="submit"
            className="searchButton"
            >
            <i className="fa fa-cog"></i>
            </button>
          <div className="modal-content">
              <label htmlFor="modal" className="close">
                  <i className="fa fa-times" aria-hidden="true"></i>
              </label>
              <header>
                  <h2>So This is a Modal</h2>
              </header>
              <article className="content">
                  <BasicTabs></BasicTabs>
              </article>
              <footer>
                  <a href="https://joshuaward.me" target="_blank" className="button success">Accept</a>
                  <label htmlFor="modal" className="button danger">Decline</label>
              </footer>
          </div>
      </div>
  )
}

export default ConfigurationModal;