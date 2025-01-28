import PersonOutlineIcon from '@mui/icons-material/PersonOutline';
import { ListGuesser,EditGuesser,ShowGuesser } from "react-admin";
import UserList from "./UsersList";
import UserEdit from "./UsersEdit";
import UserCreate from "./UsersCreate";
import UserShow from "./UsersShow";


export default {
  list: UserList,
  show: UserShow,
  create: UserCreate,
  edit: UserEdit,
  icon: PersonOutlineIcon,
  recordRepresentation: (record: any) =>
    `${record.last_name}${record.first_name}`,
};
