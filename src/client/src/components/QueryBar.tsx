import { useState } from 'react';
import axios from 'axios';
import { DocumentDto } from './DocumentIl';
import './QueryBar.css'
import ConfigurationModal from "./ConfigurationModal";
import CustomizedDialogs from "./SettingsModal";
import SettingsModal from "./SettingsModal";

export type QueryBarProps = {
  setDocumentDtos: (item: DocumentDto[]) => void;  
  setShowResults: (show: boolean) => void
}

function QueryBar(props: QueryBarProps) {

  const [query, setQuery] = useState('');

  return (
      <div className="container">
        <div className="search">
            <input
            type="text"
            className="searchTerm"
            placeholder="What are you looking for?"
            onChange={(e) => {
              setQuery(e.target.value);
              props.setShowResults(false);
            }}
            />
            <button
            type="submit"
            className="searchButton"
            onClick={async () => {
              await axios.get('http://localhost:8000/search?dataset=cranfield&query=' +
                encodeURIComponent(query))
                .then((resp) => {
                  props.setDocumentDtos(resp.data.results);
                  props.setShowResults(true);})
                .catch((err) => console.log(err.data));
            }}
            >
            <i className="fa fa-search"></i>
            </button>
            <SettingsModal></SettingsModal>
        </div>
      </div>
  );
}

export default QueryBar;
