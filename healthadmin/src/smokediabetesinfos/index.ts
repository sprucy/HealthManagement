import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import SmokediabetesinfoList from './SmokediabetesinfosList';

export default {
  list: SmokediabetesinfoList,
  show: ShowGuesser,
  edit: EditGuesser,
  icon: PersonAddAltIcon,
};
