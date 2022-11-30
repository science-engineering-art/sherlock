import axios from 'axios';
import { useState } from 'react';
import '../styles/globals.css';

export interface DocumentDto {
    doc_id: string,
    title: string,
    author: string,
    text: string,
    score: number
};

export function DocumentIl(props: DocumentDto) {
    
    // const [text, setText] = useState('');
    const [isThereText, setIsThereText] = useState(false);

    return (
        <div className='border w-11/12 rounded-md border-black-300 
        mt-4 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 
        focus:outline-none focus:ring focus:ring-blue-300'
            onClick={async () => {
                // if (text === ''){
                //     await axios.get('http://localhost:8000/document?dataset=cranfield&doc_id=' +
                //         encodeURIComponent(props.doc_id))
                //         .then((resp) => { setText('\n'+resp.data); setIsThereText(true); })
                //         .catch((err) => console.log(err.data));
                // }
                if (isThereText)
                    setIsThereText(false);
                else
                    setIsThereText(true);
            }}
        >
            <p className=''> 
                <strong>score: </strong> { props.score} 
            </p>
            <h1 className='font-bond'>
                <strong>title: </strong> { props.title }
            </h1>
            {isThereText && <p> { props.text } </p>}
        </div>
    );
}