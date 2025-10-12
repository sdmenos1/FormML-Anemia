import {
  Stethoscope,
  User,
  Calendar,
  Scale,
  Ruler,
  MapPin,
  Users,
} from "lucide-react";
import { addData } from "./api/formTask.api";
import { useForm } from "react-hook-form";
import type { people } from "./types/peopleData";
function App() {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<people>();

  const onSubmit = handleSubmit(async (data: people) => {
    await addData(data);
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-700 via-slate-600 to-slate-800 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-white rounded-lg shadow-xl border border-slate-200">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-6 rounded-t-lg">
          <div className="flex items-center gap-3 mb-2">
            <Stethoscope className="w-8 h-8 text-white" />
            <h1 className="text-2xl font-semibold text-white tracking-wide">
              Sistema de Detección Temprana
            </h1>
          </div>
          <p className="text-blue-100 text-sm">Evaluación Clínica de Anemia</p>
        </div>

        <form className="p-8" onSubmit={onSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col">
              <label
                htmlFor="email"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <Calendar className="w-4 h-4 text-blue-600" />
                Email
              </label>
              <input
                type="email"
                id="email"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                placeholder="0"
                {...register("email", { required: true })}
              />
              {errors.email && (
                <p className="text-red-500 text-xs mt-1">
                  El email es requerido
                </p>
              )}
            </div>
            <div className="flex flex-col">
              <label
                htmlFor="name"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <User className="w-4 h-4 text-blue-600" />
                Nombre Completo
              </label>
              <input
                type="text"
                id="name"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                placeholder="Ingrese nombre completo"
                {...register("name", { required: true })}
              />
              {errors.name && (
                <p className="text-red-500 text-xs mt-1">
                  El nombre es requerido
                </p>
              )}
            </div>

            <div className="flex flex-col">
              <label
                htmlFor="age"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <Calendar className="w-4 h-4 text-blue-600" />
                Edad (años)
              </label>
              <input
                type="number"
                id="age"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                placeholder="0"
                {...register("age", { required: true })}
              />
              {errors.age && (
                <p className="text-red-500 text-xs mt-1">
                  La edad es requerida
                </p>
              )}
            </div>

            <div className="flex flex-col">
              <label
                htmlFor="gender"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <Users className="w-4 h-4 text-blue-600" />
                Género
              </label>
              <select
                id="gender"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                {...register("genero", { required: true })}
              >
                <option value="">Seleccionar</option>
                <option value="masculino">Masculino</option>
                <option value="femenino">Femenino</option>
                <option value="otro">Otro</option>
              </select>
            </div>

            <div className="flex flex-col">
              <label
                htmlFor="weight"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <Scale className="w-4 h-4 text-blue-600" />
                Peso (kg)
              </label>
              <input
                type="number"
                id="weight"
                step="0.1"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                placeholder="0.0"
                {...register("peso", { required: true })}
              />
              {errors.peso && (
                <p className="text-red-500 text-xs mt-1">
                  El peso es requerido
                </p>
              )}
            </div>

            <div className="flex flex-col">
              <label
                htmlFor="height"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <Ruler className="w-4 h-4 text-blue-600" />
                Altura (cm)
              </label>
              <input
                type="number"
                id="height"
                step="0.1"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                placeholder="0.0"
                {...register("talla", { required: true })}
              />
              {errors.talla && (
                <p className="text-red-500 text-xs mt-1">
                  La altura es requerida
                </p>
              )}
            </div>

            <div className="flex flex-col">
              <label
                htmlFor="district"
                className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2"
              >
                <MapPin className="w-4 h-4 text-blue-600" />
                Distrito
              </label>
              <input
                type="text"
                id="district"
                className="px-4 py-2.5 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-slate-50"
                placeholder="Ingrese distrito"
                {...register("distrito", { required: true })}
              />
              {errors.distrito && (
                <p className="text-red-500 text-xs mt-1">
                  El distrito es requerido
                </p>
              )}
            </div>
          </div>

          <div className="mt-8 flex gap-4">
            <button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-md transition-colors duration-200 shadow-md hover:shadow-lg"
            >
              Enviar datos
            </button>
            <button
              type="reset"
              className="px-6 py-3 border border-slate-300 text-slate-700 font-medium rounded-md hover:bg-slate-50 transition-colors duration-200"
              onClick={() => {
                setValue("name", "");
                setValue("age", 0);
                setValue("genero", "");
                setValue("peso", 0);
                setValue("talla", 0);
                setValue("distrito", "");
                setValue("email", "");
              }}
            >
              Limpiar
            </button>
          </div>
        </form>

        <div className="px-8 py-4 bg-slate-50 rounded-b-lg border-t border-slate-200">
          <p className="text-xs text-slate-600 text-center">
            Se le enviara los resultados a su correo electronico
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
