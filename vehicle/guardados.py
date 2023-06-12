# if Vehicle.objects.filter(company_user=request.user, vehicle_type__icontains=valida).exists():
#             tabela = Vehicle.objects.filter(
#                 company_user=request.user, vehicle_type__icontains=valida).order_by('-created_at')
#         elif Vehicle.objects.filter(company_user=request.user, vehicle_model__icontains=valida).exists():
#             tabela = Vehicle.objects.filter(
#                 company_user=request.user, vehicle_model__icontains=valida).order_by('-created_at')
#         elif Vehicle.objects.filter(company_user=request.user, year__icontains=valida).exists():
#             tabela = Vehicle.objects.filter(
#                 company_user=request.user, year=valida)
#         elif Vehicle.objects.filter(company_user=request.user,  brand__icontains=valida).exists():
#             tabela = Vehicle.objects.filter(
#                 company_user=request.user, brand__icontains=valida).order_by('-created_at')
#         elif Vehicle.objects.filter(company_user=request.user,  chassi__icontains=valida).exists():
#             tabela = Vehicle.objects.filter(
#                 company_user=request.user, chassi__icontains=valida).order_by('-created_at')
#         elif Vehicle.objects.filter(company_user=request.user,  license_plate__icontains=valida).exists():
#             tabela = Vehicle.objects.filter(
#                 company_user=request.user, license_plate__icontains=valida).order_by('-created_at')
