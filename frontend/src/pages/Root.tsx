import { Outlet } from 'react-router-dom'

export default function Root () {
  return (
    <>
      <main>
        <div className='container mx-auto'>
          <Outlet />
        </div>
      </main>
    </>
  )
}
