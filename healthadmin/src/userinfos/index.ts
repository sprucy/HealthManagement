import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import { UserinfoList } from "./UserinfosList";

export default {
  list: UserinfoList,
  show: ShowGuesser,
  edit: EditGuesser,
  icon: PersonAddAltIcon,
};
