import '../styles/globals.css';
import logo from './img/logo.png'
import './NavBar.css'

function NavBar() {

  return (
      <div>
          <img
            className='name-engine'
            src={logo}
            alt="Logo and name of search engine"
          />
      </div>
  )
}

export default NavBar;
