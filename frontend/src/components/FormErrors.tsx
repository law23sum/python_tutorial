export default function FormErrors(props: {
  errors?: Array<{ param?: string; message: string }>;
  param?: string;
}) {
  if (!props.errors || !props.errors.length) {
    return null
  }
  const errors = props.errors.filter(error => (props.param ? error.param === props.param : error.param == null))
  if (!errors.length) {
    return null
  }
  return <ul className="text-sm text-red-500 mt-1">{errors.map((e, i) => <li key={i}>{e.message}</li>)}</ul>;
}


export function hasErrors(props: { errors?: Array<{ param?: string, message: string }>, param?: string }) {
  if (!props.errors || !props.errors.length) {
    return false
  }
  const errors = props.errors.filter(error => (props.param ? error.param === props.param : error.param == null))
  return errors.length > 0
}
