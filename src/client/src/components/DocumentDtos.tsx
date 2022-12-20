import '../styles/globals.css';
import { DocumentDto, DocumentIl } from './DocumentIl';
import { useState } from 'react';

interface DocumentDtosProps {
    items: DocumentDto[], 
    setItems: Function
}

export function DocumentDtos(props: DocumentDtosProps) {

const [isThereDocs, setIsThereDocs] = useState(true);

    return (
        <div>
            {props.items.map((item) => {
                return (
                    <DocumentIl 
                    doc_id={item.doc_id}
                    title={item.title}
                    author={item.author}
                    text={item.text}
                    score={item.score} 
                    setDocs={props.setItems} />
            );})}
            {isThereDocs && <p> Sorry, no matches for your query. </p>}
        </div> 
    );
}