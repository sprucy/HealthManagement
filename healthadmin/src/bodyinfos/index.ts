import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import BodyinfoList from './BodyinfosList';

export default {
  list: BodyinfoList,
  show: ShowGuesser,
  edit: EditGuesser,
  icon: PersonAddAltIcon,
};
