import '../styles/globals.css';

export interface SearchItem {
    title: string,
    snippet: string,
    score: number
};

export function SearchItemIl(props: SearchItem) {
    return (
        <div>
            <h1 className='font-bond'>
                { props.title }
            </h1>
            <p className=''> 
                { props.snippet } 
            </p>
        </div>
    );
}