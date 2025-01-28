import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import RiskanalysesList from './RiskanalysesList';
export default {
  list: RiskanalysesList,
  show: ShowGuesser,
  edit: EditGuesser,
  icon: PersonAddAltIcon,
};
