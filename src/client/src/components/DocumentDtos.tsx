import '../styles/globals.css';
import { DocumentDto, DocumentIl } from './DocumentIl';

interface DocumentDtosProps {
    items: DocumentDto[]
}

export function DocumentDtos(props: DocumentDtosProps) {

    return ( 
        <div>
            {props.items.map((item) => {
                return (
                    <DocumentIl 
                    doc_id={item.doc_id}
                    title={item.title}
                    author={item.author}
                    text={item.text}
                    score={item.score} />
            );})}
        </div> 
    );
}