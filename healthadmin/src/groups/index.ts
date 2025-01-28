import PeopleOutlineIcon from '@mui/icons-material/PeopleOutline';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import GroupList from './GroupsList';
import GroupEdit from './GroupsEdit';

export default {
  list: GroupList,
  edit: GroupEdit,
  icon: PeopleOutlineIcon,
};
