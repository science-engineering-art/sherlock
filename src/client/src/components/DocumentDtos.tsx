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
                    path={item.path}
                    score={item.score} />
            );})}
        </div> 
    );
}