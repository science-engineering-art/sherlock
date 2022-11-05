import '../styles/globals.css';
import { SearchItem, SearchItemIl } from './SearchItem';

interface SearchResultProps {
    items: SearchItem[]
}

export function SearchResult(props: SearchResultProps) {

    return ( 
        <div>
            {props.items.map((item) => {
                return (
                    <SearchItemIl 
                    title={item.title} 
                    snippet={item.snippet} 
                    score={item.score} />
            );})}
        </div> 
    );
}