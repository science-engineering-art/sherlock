import axios from 'axios';
import { useState } from 'react';
import '../styles/globals.css';
import './DocumentIl.css'

export interface DocumentDto {
    doc_id: string,
    title: string,
    author: string,
    text: string,
    score: number,
    setDocs: Function
};

export function DocumentIl(props: DocumentDto) {
    
    const [isThereText, setIsThereText] = useState(false);

    return (
        <div className='document-container'
            onClick={async () => {
                if (isThereText)
                    setIsThereText(false);
                else
                    setIsThereText(true);
            }}
        >
            <h1 className='document-title'>
                <strong>title: </strong> { props.title }
            </h1>
            
            {isThereText && <DocumentText 
                doc_id={props.doc_id} 
                text={props.text} 
                setDocs={props.setDocs}
            />} 
            
            <p className='score'>
                <strong>score: </strong> { props.score }
            </p>
        </div>
    );
}

interface DocText {
    text: string,
    doc_id: string,
    setDocs: Function
}

function DocumentText(props: DocText) {
    
    async function feedback(is_relevant: boolean) {
        var model: string = sessionStorage['model']
        var dataset: string = sessionStorage['dataset']
        var query: string = sessionStorage['query']
        
        await axios.get('http://localhost:8000/feedback?model='+ encodeURIComponent(model) + 
            '&dataset=' + encodeURIComponent(dataset) + '&query=' + encodeURIComponent(query) + 
            '&doc_id=' + encodeURIComponent(props.doc_id) + '&is_rel=' + encodeURIComponent(is_relevant))
            .then((resp) => {
                props.setDocs(resp.data.results)
            }).catch((err) => console.log(err.data));
    }
    
    return (
        <div className='document-text' 
            onClick={(e)=>e.stopPropagation()}
        >
            <p> {props.text} </p>

            {sessionStorage['model'] === 'vector' && 
            <div>
                <strong> Do you consider the document to be relevant? </strong>
                <button className='button-rel' onClick={async () => feedback(true)}>Yes</button> 
                <button className='button-nrel' onClick={async () => feedback(false)}>No</button>
            </div>}
        </div>
    );
}