import {Outlet} from "react-router-dom";
import DashboardLayout from "../../components/DashboardLayout.tsx";


export default function Dashboard() {
  return (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  );
}
