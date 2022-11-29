import axios from 'axios';
import { useState } from 'react';
import '../styles/globals.css';
import './DocumentIl.css'

export interface DocumentDto {
    doc_id: string,
    title: string,
    author: string,
    text: string,
    score: number
};

export function DocumentIl(props: DocumentDto) {
    
    const [text, setText] = useState('');
    const [isThereText, setIsThereText] = useState(false);

    return (
        <div className='document-container'
            onClick={async () => {
                if (text === ''){
                    await axios.get('http://localhost:8000/document?doc_id=' +
                        encodeURIComponent(props.doc_id))
                        .then((resp) => { setText('\n'+resp.data); setIsThereText(true); })
                        .catch((err) => console.log(err.data));
                }
                if (isThereText)
                    setIsThereText(false);
                else
                    setIsThereText(true);
            }}
        >
            <h1 className='document-title'>
                <strong>title: </strong> { props.title }
            </h1>
            {isThereText && <p className='document'> {text} </p>}
            <p className='score'>
                <strong>score: </strong> { props.score }
            </p>
        </div>
    );
}