import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import BcholesterinList from './BcholesterinsList';
export default {
  list: BcholesterinList,
  show: ShowGuesser,
  edit: EditGuesser,
  icon: PersonAddAltIcon,
};
