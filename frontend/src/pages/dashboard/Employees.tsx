import {PegasusApi} from "api-client";
import EmployeeApplication from "assets/javascript/pegasus/examples/react/App.jsx";
import {getApiConfiguration} from "../../api/utils.tsx";
import emptyImage from '/undraw_empty.svg'

export default function EmployeeApp() {
  const client = new PegasusApi(getApiConfiguration());

  return (
    <EmployeeApplication client={client} urlBase="/dashboard/employees" emptyImage={emptyImage}/>
  );
}
